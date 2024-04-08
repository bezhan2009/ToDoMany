/*TO DO: Решить проблему с картками */

import Button from "../../components/UI/button/Button";
import EnviromentCard from "../../components/EnviromentCard";

import "./Home.css";

export default function Home() {
  return (
    <section className="main-section">
      <article className="top-btn">
        <Button mode="outline" className="add-new-enviroment-btn">
          +
        </Button>
        <Button mode="field">Подключиться к окружению</Button>
      </article>
      <div className="card-container">
        <EnviromentCard
          title="Работа в айти"
          img="https://placehold.co/56x56"
          description="Lorem ipsum dolor sit amet consectetur. In commodo varius lacinia suspendisse."
        />
        <EnviromentCard
          title="Работа в айти"
          img="https://placehold.co/56x56"
          description="Lorem ipsum dolor sit amet consectetur. In commodo varius lacinia suspendisse."
        />
        <EnviromentCard
          title="Работа в айти"
          img="https://placehold.co/56x56"
          description="Lorem ipsum dolor sit amet consectetur. In commodo varius lacinia suspendisse."
        />
        <EnviromentCard
          title="Работа в айти"
          img="https://placehold.co/56x56"
          description="Lorem ipsum dolor sit amet consectetur. In commodo varius lacinia suspendisse.Lorem ipsum dolor sit amet consectetur. In commodo varius lacinia suspendisse.Lorem ipsum dolor sit amet consectetur. In commodo varius lacinia suspendisse.Lorem ipsum dolor sit amet consectetur. In commodo varius lacinia suspendisse.Lorem ipsum dolor sit amet consectetur. In commodo varius lacinia suspendisse."
        />
        <EnviromentCard
          title="Работа в айти"
          img="https://placehold.co/56x56"
          description="Lorem ipsum dolor sit amet consectetur. In commodo varius lacinia suspendisse."
        />
        <EnviromentCard
          title="Работа в айти"
          img="https://placehold.co/56x56"
          description="Lorem ipsum dolor sit amet consectetur. In commodo varius lacinia suspendisse."
        />
      </div>
    </section>
  );
}
