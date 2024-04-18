import style from "./EnviromentCard.module.scss"

export default function EnviromentCard({ title, img, description }) {
    return (
      <div className={style.card}>
        <div className={style.header}>
          <h1 className={style.title}>{title}</h1>
          <img src={img} alt={title} />
        </div>
        <div className={style.description}>
          <h4 className={style.text}>{description}</h4>
        </div>
      </div>
    );
  }
  