# Bilingual Toggle Pattern

Use this pattern whenever the rebuilt deck needs a language toggle.

## DOM Pattern

```html
<button class="lang-toggle" id="langToggle" data-active-lang="zh" aria-live="polite">
  EN / 中
</button>

<div class="copy-stack" data-copy-block>
  <div class="copy-layer is-active" data-lang="zh">中文内容</div>
  <div class="copy-layer" data-lang="en" aria-hidden="true">English content</div>
</div>
```

## CSS Pattern

```css
.copy-stack {
  display: grid;
}

.copy-layer {
  grid-area: 1 / 1;
  opacity: 0;
  visibility: hidden;
  transition: opacity 180ms ease;
}

.copy-layer.is-active {
  opacity: 1;
  visibility: visible;
}

.lang-toggle {
  position: sticky;
  top: 1rem;
  z-index: 40;
}
```

Notes:

- keep the zh and en layers inside the same width container
- use grid overlay so the container footprint stays stable during toggles
- avoid `display: none` as the primary toggle mechanism when it causes layout jumps

## JavaScript Pattern

```js
const button = document.querySelector('#langToggle');
const layers = document.querySelectorAll('[data-lang]');

button?.addEventListener('click', () => {
  const next = button.dataset.activeLang === 'zh' ? 'en' : 'zh';
  button.dataset.activeLang = next;
  document.documentElement.dataset.lang = next;

  layers.forEach((layer) => {
    const active = layer.dataset.lang === next;
    layer.classList.toggle('is-active', active);
    layer.setAttribute('aria-hidden', String(!active));
  });
});
```

## Hard Rules

- toggle button must remain visible in playback mode
- both language layers must share the same structural container width
- if zh and en produce different title line counts, rewrite or widen before shrinking type
