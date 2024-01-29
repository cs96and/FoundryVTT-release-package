# FoundryVTT-release-package
GitHub action to publish a FoundyVTT package using the [Package Release API](https://foundryvtt.com/article/package-release-api/)

### Mandatory Inputs
- `package-token`: The secret token of your package for the FoundryVTT Package Release API
- `manifest-url`: The URL of the JSON manifest of your package.  **Please Note**: This is not the package manifest URL in your package manifest, which should be pointed to a latest branch. Instead, it should point to a specific release to allow users to download this specific version of your package.

### Optional Inputs
- `version`: The version of the release.  Leave undefined to use the `version` entry from your manifest file.
- `notes-url`: The URL of the release notes for this release of your package.  Leave undefined to use the `changelog` entry from your manifest file.
- `dry-run`: Set to any value apart from `false` or `0` to do a dry-run.  Leave undefined or set to `false` or `0` for a proper release.

### Outputs
- `response-code`: The HTTP response code
- `response-json`: The JSON response

## Example
```yaml
  - name: Publish Module to FoundryVTT Website
    id: publish-to-foundry-website
    uses: cs96and/FoundryVTT-release-package@v1
    with:
      package-token: ${{ secrets.PACKAGE_TOKEN }}
      manifest-url: https://github.com/${{github.repository}}/releases/download/${{github.event.release.tag_name}}/module.json
```
