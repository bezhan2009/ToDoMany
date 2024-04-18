import EnviromentCard from "./enviromentCard/EnviromentCard";
import TaskCard from "./taskCard/TaskCard";

export default function RenderCard({
  cardMode,
  title,
  img,
  description,
  state,
}) {
  /* TO DO: Ubdate this construction to redux slice */

  const TASK = "task";
  const ENVIROMENT = "enviroment";

  switch (cardMode) {
    case TASK:
      return (
        <TaskCard title={title} description={description} state={state} />
      );
    case ENVIROMENT:
      return (
        <EnviromentCard title={title} img={img} description={description} />
      );
    default:
      return null;
  }
}
