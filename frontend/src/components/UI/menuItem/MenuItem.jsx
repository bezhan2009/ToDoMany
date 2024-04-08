import Button from "../button/Button";
import style from "./MenuItem.module.css";

export default function MenuItem({ mode, partialOpen, icon, label, to }) {
  let navbarContent = <img src={icon} alt={label} />;
  if (partialOpen) {
    navbarContent = (
      <div className={style["nav-item-wrapper"]}>
        <img
          src={icon}
          alt={label}
          className={[style["nav-item-img"]]}
        />
        <span>{label}</span>
      </div>
    );
  }

  const ariaLabel = `Navbar ${label ? `${label}` : ""} button`;

  return (
    <li>
      {/* Заменить на Link BrowserRouter*/}
      <a href={to}>
        <Button mode={mode} aria-label={ariaLabel}>
          {navbarContent}
        </Button>
      </a>
    </li>
  );
}
