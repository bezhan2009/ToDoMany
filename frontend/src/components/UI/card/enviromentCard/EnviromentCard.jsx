import { Link } from "react-router-dom";
import style from "./EnviromentCard.module.scss";

export default function EnviromentCard({ title, img, description, path }) {
  return (
    <div className={style.card}>
      <Link to={path} className={style.link}>
        <div className={style.header}>
          <h1 className={style.title}>{title}</h1>
          <img src={img} alt={title} />
        </div>
        <div className={style.description}>
          <h4 className={style.text}>{description}</h4>
        </div>
      </Link>
    </div>
  );
}
