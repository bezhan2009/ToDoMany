/*TO DO: Обновить стили */

import classNames from "classnames";
import PropTypes from "prop-types";

import styles from "./Button.module.scss";

export default function Button({
  children,
  className,
  mode,
  size,
  Icon,
  onClick,
  disabled,
  ...rest
}) {
  PropTypes.checkPropTypes(
    {
      mode: PropTypes.oneOf([
        "nav",
        "primary",
        "secondary",
        "tertiary",
        "outline",
        "field",
        "disabled-nav"
      ]),
      size: PropTypes.oneOf(["sm", "medium", "l"]),
      Icon: PropTypes.node,
      onClick: PropTypes.func,
      disabled: PropTypes.bool,
    },
    { mode, size, Icon, onClick, disabled },
    "prop",
    "Button"
  );

  const cssClasses = classNames(
    styles.button,
    styles[mode],
    styles[size],
    { [styles.disabled]: disabled },
    className
  );

  return (
    <button
      className={cssClasses}
      onClick={onClick}
      disabled={disabled}
      {...rest}
    >
      {Icon && <span className={styles["button-icon"]}>{Icon}</span>}
      {children}
    </button>
  );
}

Button.defaultProps = {
  className: "",
  mode: "primary",
  size: "medium",
  Icon: null,
  onClick: () => {},
  disabled: false,
};

Button.propTypes = {
  children: PropTypes.node.isRequired,
  className: PropTypes.string,
  mode: PropTypes.oneOf([
    "nav",
    "primary",
    "secondary",
    "tertiary",
    "outline",
    "field",
    "disabled-nav",
  ]),
  size: PropTypes.oneOf(["sm", "medium", "l"]),
  Icon: PropTypes.node,
  onClick: PropTypes.func,
  disabled: PropTypes.bool,
};
