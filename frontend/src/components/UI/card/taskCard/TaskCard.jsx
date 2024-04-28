import Button from "../../button/Button";
import styles from "./TaskCard.module.scss";

export default function TaskCard({ title, description, state }) {
  return (
    <div className={styles.card}>
      <div className={styles.header}>{title}</div>
      <div className={styles.description}>{description}</div>
      <div className={styles.bottom}>
        <div className={styles.date}>Срок: {state}</div>
        <Button>Выполнить задание</Button>
      </div>
    </div>
  );
}
