import MenuToggleSwitch from "./UI/menuToggle/MenuToggleSwitch";
import Button from "./UI/button/Button";
import NavigationBar from "./NavigationBar";

export default function Header({
  onChangeHeaderToggleSwitch,
  menuOpen,
  nameOfPage,
}) {
  return (
    <>
    <header className="header">
      <div className="header-float-left">
        <MenuToggleSwitch
          checked={menuOpen}
          onChangeState={onChangeHeaderToggleSwitch}
        />
        <h1 className="header-page-name">{nameOfPage}</h1>
      </div>
      <div className="header-float-right">
        <Button
          Icon={<img src="https://placehold.co/20x20" alt="settings" />}
          aria-label="Settings button"
        />
      </div>
    </header>
    <NavigationBar partialOpen={menuOpen} />
    </>
  );
}
