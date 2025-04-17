# Shopify Store Project

This directory contains your Shopify store code and theme.

## Prerequisites

- Node.js (v14+)
- npm or Yarn
- Shopify CLI (`@shopify/cli`)

## Setup

1. Install Shopify CLI:
   ```bash
   npm install -g @shopify/cli
   ```

2. Login to your Shopify store:
   ```bash
   shopify login --store=your-store.myshopify.com
   ```

3. Scaffold a new theme (Liquid/Dawn):
   ```bash
   shopify theme init my-theme --template=demo-theme
   ```

4. Enter the theme directory:
   ```bash
   cd my-theme
   ```

5. Start local development server:
   ```bash
   shopify theme serve
   ```

6. When ready to publish:
   ```bash
   shopify theme push --allow-live
   ```

## Next Steps

- Customize theme templates, CSS, and JavaScript under `sections/`, `templates/`, `assets/`.
- Commit changes and, optionally, set up CI/CD (e.g., GitHub Actions).

For assistance with theme customization, refer to the Shopify Theme Development documentation.