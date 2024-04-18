import React from "react";
import classNames from "classnames";
import PropTypes from "prop-types";
import styles from "./Button.module.scss";

function Button({
  children,
  className,
  mode,
  Icon,
  "aria-label": ariaLabel,
  "aria-labelledby": ariaLabelledBy,
  ...props
}) {
  const cssClasses = classNames(
    styles.button,
    {
      [styles[`${mode}-button`]]: mode,
    },
    className
  );

  return (
    <button
      className={cssClasses}
      type="button"
      aria-label={ariaLabel || ariaLabelledBy || "Button"}
      aria-labelledby={ariaLabelledBy}
      {...props}
    >
      {Icon && (
        <span className={styles["button-icon"]} style={{ fontSize: "1.5rem" }}>
          {Icon}
        </span>
      )}
      {children}
    </button>
  );
}

Button.propTypes = {
  children: PropTypes.node,
  className: PropTypes.string,
  mode: PropTypes.string,
  Icon: PropTypes.element,
  "aria-label": PropTypes.string,
  "aria-labelledby": PropTypes.string,
};

Button.defaultProps = {
  className: "",
  mode: "",
  Icon: null,
};

export default Button;
