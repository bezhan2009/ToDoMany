import { useParams } from "react-router-dom";
import RenderCard from "../../components/UI/card/CardController";

export default function EnviromentPage() {
  //получение значения id из URL-адреса
  const { id } = useParams();

  return (
    <div>
      enviroment task: ${id}
      <RenderCard
        cardMode="task"
        title="Сделать аунтификацию"
        description="Дима, ты у нас отвечаешь за аунтификацию. Нужно сделать до завтра!!!"
        state="Завтра"
      />
    </div>
  );
}
