import Button from "../button/Button";
import style from "./MenuToggleSwitch.module.scss";

export default function MenuToggleSwitch({ checked, onChangeState }) {
  const switchClass = checked ? style.close : style.burger;
  const switchClasses = `${style.switch} ${switchClass}`;

  return (
    <Button className={switchClasses} onClick={onChangeState}>
      <span className={style.top}></span>
      <span className={style.middle}></span>
      <span className={style.bottom}></span>
    </Button>
  );
}
