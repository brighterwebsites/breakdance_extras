---
name: wp-mcp-oauth-fix
description: >
  Fix broken or missing MCP OAuth connections on WordPress sites using the
  Agent Connector for WP (acfw) plugin. Use when a wp-* MCP server shows
  needsAuth, invalid_client, Unknown client_id, invalid_redirect_uri, or a
  blank CLIENT_ID in ~/.cursor/mcp.json. Covers: stale client_id removal,
  Cursor redirect_uri registration, mu-plugin for cursor:// scheme, and
  manual DB insert workflow.
disable-model-invocation: true
---

# Fix WordPress MCP OAuth (acfw / Agent Connector for WP)

## Background

All `wp-*.com.au` entries in `~/.cursor/mcp.json` use the same pattern:

```json
"wp-site.com.au": {
  "url": "https://site.com.au/wp-json/mcp/mcp-adapter-default-server",
  "auth": {
    "CLIENT_ID": "32hexchars",
    "scopes": ["mcp:tools", "mcp:read", "mcp:write"]
  }
}
```

The OAuth server is `acfw-auth/v1` (registered by Agent Connector for WP). Cursor
uses `http://localhost:8787/callback` as its redirect_uri for MCP OAuth. The plugin
accepts `http://localhost` URIs natively, so a standard curl registration works.

> If unsure of Cursor's exact redirect_uri: start Connect in Cursor, let it open the
> browser, and copy the `redirect_uri=` value from the address bar.

---

## Step 1 — Identify the failure mode

Check `~/.cursor/mcp.json` and the Cursor log:

```
C:\Users\vanes\AppData\Roaming\Cursor\logs\<session>\window5\mcp-server-user-wp-<site>.workbench.log
```

| Symptom | Cause |
|---------|-------|
| `invalid_client` / `Unknown client_id` | CLIENT_ID in mcp.json is stale/dead |
| `invalid_redirect_uri` (HTTP 400) | Plugin is rejecting `cursor://` scheme at DCR |
| `statusType=needsAuth`, no browser opens | CLIENT_ID is pinned to a dead value |
| `statusType=initializing` then 400 | CLIENT_ID was cleared; DCR ran but was rejected |

---

## Step 2 — Clear the stale CLIENT_ID

In `~/.cursor/mcp.json`, set `"CLIENT_ID": ""` for the affected site.
Leave all other sites untouched.

This puts the server into `initializing` state so Cursor will attempt DCR on
the next connect — which will fail (step 3 explains why) but is required to
unblock the flow.

---

## Step 3 — Check the mu-plugin exists on the site

The plugin's `is_valid_redirect_uri` and the authorize/token endpoints all call
`esc_url_raw()` which strips the `cursor://` scheme. A mu-plugin fixes all three
places without touching the plugin source.

SSH to the site and check:

```bash
cat /home/<domain>/public_html/wp-content/mu-plugins/allow-cursor-oauth.php
```

If missing, create it:

```bash
echo PD9waHAKYWRkX2ZpbHRlciggJ2tzZXNfYWxsb3dlZF9wcm90b2NvbHMnLCBzdGF0aWMgZnVuY3Rpb24gKCBhcnJheSAkcHJvdG9jb2xzICk6IGFycmF5IHsKICAgICRwcm90b2NvbHNbXSA9ICdjdXJzb3InOwogICAgcmV0dXJuICRwcm90b2NvbHM7Cn0gKTs= \
  | base64 -d > /home/<domain>/public_html/wp-content/mu-plugins/allow-cursor-oauth.php
```

Contents (for reference):
```php
<?php
add_filter( 'kses_allowed_protocols', static function ( array $protocols ): array {
    $protocols[] = 'cursor';
    return $protocols;
} );
```

---

## Step 4 — Register the Cursor client via curl

`http://localhost:8787/callback` passes the plugin's built-in `http://localhost`
validation, so use the REST endpoint directly — no DB workaround needed:

```bash
curl -s -X POST https://<domain>/wp-json/acfw-auth/v1/register \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "Cursor",
    "redirect_uris": ["http://localhost:8787/callback"],
    "grant_types": ["authorization_code", "refresh_token"],
    "response_types": ["code"],
    "token_endpoint_auth_method": "none"
  }'
```

Copy the `client_id` from the JSON response.

> **If curl gives `invalid_redirect_uri`:** Cursor's port changed. Start Connect in
> Cursor, let the browser open, copy the `redirect_uri=` value from the address bar,
> and re-register with that exact value.

---

## Step 5 — Update mcp.json

Put the generated `client_id` back into `~/.cursor/mcp.json`:

```json
"wp-site.com.au": {
  "url": "https://site.com.au/wp-json/mcp/mcp-adapter-default-server",
  "auth": {
    "CLIENT_ID": "<generated_client_id>",
    "scopes": ["mcp:tools", "mcp:read", "mcp:write"]
  }
}
```

---

## Step 6 — Browser approval (manual)

1. Cursor **Settings → MCP → `wp-site.com.au` → Connect**
2. Browser opens to WordPress OAuth authorize page
3. Log in as the site's admin user and approve the three scopes
4. Cursor writes the token; server moves from `initializing` → `connected`

> If you need a specific WP user: `wp user get <username> --fields=ID,user_login,roles --allow-root`

---

## Verification

Check the log for success:
```
mcp-server-user-wp-<site>.workbench.log
→ statusType=connected
```

Or call `GetDynamicTools` on the namespace — if tools list is returned, it's live.

---

## SSH key convention

Site SSH keys are at `~/.ssh/ssh-<sitename>` (e.g. `ssh-coastalnativesupply`).
SSH user format: `<prefix><digits>@host4.bweb1.com.au` (check the seo-command-center CLAUDE.md for each site).
WP root: `/home/<domain>/public_html/`

---

## Notes

- **Claude.ai connector** registers separately with `https://claude.ai/api/mcp/auth_callback` — leave it alone when working on Cursor clients.
- If `wp_acfw_oauth_clients` table doesn't exist: deactivate/reactivate the plugin to create it.
- If the mu-plugins directory doesn't exist: `mkdir -p /home/<domain>/public_html/wp-content/mu-plugins/`
- The plugin version that introduced strict redirect_uri validation is v1.30.0+ — older installs may still accept `cursor://` via DCR without the mu-plugin.
