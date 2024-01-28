# FoundryVTT-release-package
GitHub action to publish a FoundyVTT package using the [Package Release API](https://foundryvtt.com/article/package-release-api/)

### Inputs
- `package-token`: The secret token of your package for the FoundryVTT Package Release API
- `manifest-url`: The URL of the JSON manifest of your package.  **Please Note**: This is not the package manifest URL in your package manifest, which should be pointed to a latest branch. Instead, it should point to a specific release to allow users to download this specific version of your package.

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
