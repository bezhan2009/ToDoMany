import Button from "@components/UI/button/Button";
import RenderCard from "@components/UI/card/CardController";
import HomeSceleton from "./Home.sceleton.jsx";

import "./Home.scss";

export default function Home() {
  /* HARDCODE TO USE SCELETON AND VISUAL CARD */
  const isLoading = true;
  const ARRAYLENGTH = 20;

  if (!isLoading) {
    return <HomeSceleton />;
  }

  return (
    <section className="enviroment-section">
      <article className="top-btn">
        <Button mode="outline" className="add-new-enviroment-btn">
          +
        </Button>
        <Button mode="field">Подключиться к окружению</Button>
      </article>
      <ul className="card-container">
        {[...Array(ARRAYLENGTH)].map((_, index) => (
          <li
            className="card-item"
            key={index}
          >
            <RenderCard
              path={`/demo/api/enviroment/${index}`}
              cardMode="enviroment"
              title="Работа в айти"
              img="https://placehold.co/56x56"
              description="Lorem ipsum dolor sit amet consectetur. In commodo varius lacinia suspendisse."
            />
          </li>
        ))}
      </ul>
    </section>
  );
}
