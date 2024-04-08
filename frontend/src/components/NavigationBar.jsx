import MenuItem from "./UI/menuItem/MenuItem";
import homeIco from "../assets/lucide_home.png";
import tasksIco from "../assets/iconoir_task-list.png";
import calendarIco from "../assets/calendar.png";

export default function NavigationBar({ partialOpen }) {
  return (
    <nav className={`navigation-bar ${partialOpen ? "partial-open" : ""}`}>
      <div className="route-nav-item">
        <ul>
          <MenuItem
            partialOpen={partialOpen}
            icon={homeIco}
            label="Главная страница"
            mode="nav"
            to="/"
          />
          <MenuItem
            partialOpen={partialOpen}
            label="Календарь"
            icon={calendarIco}
            mode="nav"
            to="/calendar"
          />
        </ul>
      </div>
      <div className="dynamical-nav-item">
        <ul>
          <MenuItem
            partialOpen={partialOpen}
            label="Список заданий"
            icon={tasksIco}
            mode="disabled-nav"
          />
          {/* 
            Это тупой (статический) метод отображения,
            перехода по двум пунктам окружения.
          */}
          {[...Array(2)].map((_, index) => (
            <MenuItem
              key={index}
              id={index}
              partialOpen={partialOpen}
              icon="https://placehold.co/18x20"
              mode="nav"
              to={`/demo/api/environment/admin/action/${index}`}
            />
          ))}
        </ul>
      </div>
    </nav>
  );
}
