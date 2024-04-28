import { Link } from "react-router-dom";
import Button from "../button/Button";
import style from "./MenuItem.module.scss";

export default function MenuItem({ mode, partialOpen, icon, label, to }) {
  let navbarContent = (
    <img src={icon} alt={label} className={[style["nav-item-img"]]} />
  );
  if (partialOpen) {
    navbarContent = (
      <div className={style["nav-item-wrapper"]}>
        <img src={icon} alt={label} className={[style["nav-item-partial"]]} />
        <span>{label}</span>
      </div>
    );
  }

  return (
    <li>
      <Link to={to}>
        <Button mode={mode}>
          {navbarContent}
        </Button>
      </Link>
    </li>
  );
}
