// deterministic animation helpers — everything is a pure function of frame f
const clamp01 = t => Math.min(1, Math.max(0, t));
// progress 0..1 across frames [a,b)
const rng = (f, a, b) => clamp01((f - a) / (b - a));
const easeOut = t => 1 - Math.pow(1 - t, 4);       // snappy settle
const easeInOut = t => t < 0.5 ? 4*t*t*t : 1 - Math.pow(-2*t + 2, 3) / 2;
const lerp = (a, b, t) => a + (b - a) * t;
const $ = id => document.getElementById(id);

// slide-up + fade entrance for element, over frames [a,b), from dy px
function enter(el, f, a, b, dy = 40) {
  const t = easeOut(rng(f, a, b));
  el.style.opacity = t;
  el.style.transform = `translateY(${(1 - t) * dy}px)`;
}
// fade whole stage out over [a,b)
function exitFade(el, f, a, b) {
  if (f >= a) el.style.opacity = Math.min(parseFloat(el.style.opacity || 1), 1 - rng(f, a, b));
}
// counter text
function count(el, f, a, b, from, to, fmt) {
  const v = lerp(from, to, easeOut(rng(f, a, b)));
  el.textContent = fmt(v);
}
const fmtInt = v => Math.round(v).toLocaleString('en-US');
// svg path draw-on: set once with prepDraw, animate with draw()
function prepDraw(path) {
  const L = path.getTotalLength();
  path.style.strokeDasharray = L;
  path.dataset.len = L;
  return L;
}
function draw(path, f, a, b) {
  path.style.strokeDashoffset = (1 - easeInOut(rng(f, a, b))) * path.dataset.len;
}
