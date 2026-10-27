import { demoCharacters } from "./features/roster/demoCharacters";

export default function App() {
  return (
    <main className="workspace">
      <header className="topbar">
        <a className="brand" href="#roster" aria-label="Character Manager home">
          <span className="brand__mark" aria-hidden="true">✦</span>
          <span>Character Manager</span>
        </a>
        <span className="topbar__tag">Player workspace</span>
      </header>

      <section className="intro" id="roster" aria-labelledby="page-title">
        <p className="eyebrow">Your table, at a glance</p>
        <div className="intro__row">
          <div>
            <h1 id="page-title">Character roster</h1>
            <p className="lede">Keep your adventurers close. Pick up where the story left off.</p>
          </div>
          <span className="roster-count">{demoCharacters.length} characters</span>
        </div>
      </section>

      <aside className="preview-note" role="note">
        <span aria-hidden="true">◈</span>
        <p><strong>Preview screen</strong> — showing sample characters. This React preview does not access or change your saved data.</p>
      </aside>

      <section className="roster" aria-label="Sample character roster">
        {demoCharacters.map((character) => (
          <article className="character-card" key={character.id}>
            <div className={`character-card__portrait character-card__portrait--${character.tone}`} aria-hidden="true">
              <span>{character.initial}</span>
            </div>
            <div className="character-card__body">
              <div className="character-card__heading">
                <div>
                  <p className="character-card__eyebrow">Level {character.level} · {character.ruleset}</p>
                  <h2>{character.name}</h2>
                  <p className="character-card__class">{character.ancestry} {character.className}</p>
                </div>
                <span className="card-arrow" aria-hidden="true">↗</span>
              </div>
              <div className="character-card__stats" aria-label="Combat summary">
                <div><span>Hit points</span><strong>{character.hpCurrent}<i> / {character.hpMaximum}</i></strong></div>
                <div><span>Armor class</span><strong>{character.armorClass}</strong></div>
                <div><span>Speed</span><strong>{character.speed}<i> ft.</i></strong></div>
              </div>
              <div className="hp-track" aria-hidden="true"><span style={{ width: `${Math.round(character.hpCurrent / character.hpMaximum * 100)}%` }} /></div>
            </div>
          </article>
        ))}
      </section>
      <footer className="workspace__footer">An early React preview · Your current character app remains available as before</footer>
    </main>
  );
}
