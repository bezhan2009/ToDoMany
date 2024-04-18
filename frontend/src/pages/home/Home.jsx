import { Link } from "react-router-dom";
import Button from "@components/UI/button/Button";
import RenderCard from "@components/UI/card/CardController";
import HomeSceleton from "./Home.sceleton.jsx";

import "./Home.scss";

export default function Home() {
  /* HARDCODE TO USE SCELETON */
  const isLoading = true;
  if (!isLoading) {
    return <HomeSceleton />;
  }

  return (
    <section className="main-section">
      <article className="top-btn">
        <Button mode="outline" className="add-new-enviroment-btn">
          +
        </Button>
        <Button mode="field">Подключиться к окружению</Button>
      </article>
      <ul className="card-container">
        {[...Array(2)].map((_, index) => (
          <li className="card-item" key={index}>
            <Link to={`/demo/api/enviroment/${index}`} className="card-link">
              <RenderCard
                cardMode="enviroment"
                title="Работа в айти"
                img="https://placehold.co/56x56"
                description="Lorem ipsum dolor sit amet consectetur. In commodo varius lacinia suspendisse."
              />
            </Link>
          </li>
        ))}
      </ul>
    </section>
  );
}
