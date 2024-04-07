import MenuItem from "./UI/menuItem/MenuItem";

export default function NavigationBar({ partialOpen }) {
  return (
    <nav className={`navigation-bar ${partialOpen ? "partial-open" : ""}`}>
      <div className="route-nav-item">
        <ul>
          <MenuItem
            partialOpen={partialOpen}
            icon="https://placehold.co/18x20"
            label="Главная страница"
            mode="nav"
            to="/"
          />
          <MenuItem
            partialOpen={partialOpen}
            icon="https://placehold.co/18x20"
            label="Календарь"
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
            icon="https://placehold.co/18x20"
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
