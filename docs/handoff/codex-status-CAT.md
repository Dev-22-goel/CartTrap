# CAT warehouse catalog status

**Status:** Catalog merge and guarded product detail implemented and verified offline. Storefront activation is pending the listing-owner change below.

- `src/catalog.ts` merges warehouse variants with Shopify through `searchCatalog(query, { includeWarehouse: true })`. Each warehouse variant has a separate `wh:type-…-v…` ID, a source label, USD pricing, and image, video, and audio URLs. The projection omits dataset attack labels. The existing generator type table supplies product types when the dataset API omits them, including `Multivitamins` for the Livingood demo item.
- `src/components/ProductPage.tsx` resolves warehouse detail links, shows the gallery, audio and plain-text description, and invokes the live protected `useAgentRun` path. The local cart mutation requires a completed approval. Holds, escalations, missing verdicts, transport errors, and missing uploads leave the cart alone. The page renders `FraudCard` from the guarded run and forwards `state.evidence` when the UI lane supplies it.
- `src/api.ts` and `src/lib/dataset.ts` build the guarded multipart request from the dataset request, budget, real Shopify product ID, and the listing's image, video, and audio blobs.

## Storefront follow-up

`src/components/ShopYourself.tsx` is outside CAT's assigned files. Its quick-add handler calls `cart.add` directly. Before enabling the warehouse merge there, route warehouse quick-add to `onOpenProduct(p)` and show source badges using `p.source`. Pass `includeWarehouse: true` from its storefront searches after the handler is wired. Until then, the shared search defaults to its existing Shopify behavior. Approval to edit the file and a CAT ADR number were requested. The brief assigns ADR 0025 to EV and gives CAT no number. All implementation edits are within CAT's assigned files.

## Verification

```text
> npx.cmd --offline --no-install vitest run
Test Files  5 passed (5)
     Tests  70 passed (70)

> npx.cmd --offline --no-install tsc -b --noEmit
[exit 0, no diagnostics]
```

The tests mock the storefront feeds and run response, and check whole-word search, canonical IDs, the guarded multipart payload, missing media, approved adds, held adds, and runs without a verdict. Live services and evidence rendering across lanes are unverified. No Git commands were run.
