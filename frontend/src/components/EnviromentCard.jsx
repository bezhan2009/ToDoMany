export default function EnviromentCard({title, img, description}) {
  return (
    <div className="enviroment-card">
      <article className="enviroment-card-header">
        <h1 className="enviroment-card-tittle">{title}</h1>
        <img src={img} alt={title} />
      </article>
      <div className="enviroment-card-description">
        <h4 className="enviroment-card-text">
          {description}
        </h4>
      </div>
    </div>
  );
}
