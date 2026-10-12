"""Riallinea sottolineature e note dopo una correzione autorizzata dell'URL."""
import json


def render_script(aliases):
    if not aliases:
        return ''
    mapping = json.dumps(aliases, ensure_ascii=True).replace('<', '\\u003c')
    return '<script data-quote-url-migration>\n' + SCRIPT.replace('__ALIASES__', mapping) + '\n</script>\n'


SCRIPT = """(function () {
  try {
    var aliases = __ALIASES__;
    var underlined = JSON.parse(localStorage.getItem('sottolineature-underlined') || '[]');
    var notes = JSON.parse(localStorage.getItem('sottolineature-notes') || '{}');
    var noteChanged = false;
    if (notes && typeof notes === 'object' && !Array.isArray(notes)) {
      Object.keys(aliases).forEach(function (oldSlug) {
        var newSlug = aliases[oldSlug];
        if (Object.prototype.hasOwnProperty.call(notes, oldSlug) &&
            !Object.prototype.hasOwnProperty.call(notes, newSlug)) {
          notes[newSlug] = notes[oldSlug];
          noteChanged = true;
        }
      });
      if (noteChanged) localStorage.setItem('sottolineature-notes', JSON.stringify(notes));
    }
    if (Array.isArray(underlined) && underlined.some(function (slug) { return aliases[slug]; })) {
      underlined = underlined.map(function (slug) { return aliases[slug] || slug; })
        .filter(function (slug, index, list) { return list.indexOf(slug) === index; });
      localStorage.setItem('sottolineature-underlined', JSON.stringify(underlined));
    }
  } catch (e) {}
})();"""
