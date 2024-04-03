import styles from "./TaskTemp.module.scss";

export function TaskTemp({ taskStatus }) {
    let taskTemp = "";

    switch (taskStatus) {
        case "active":
            taskTemp = "завтра";
            break;
        case "completed":
            taskTemp = "выполнено";
            break;
        case "overdue":
            taskTemp = "исчерпан";
            break;
        default:
            taskTemp = "";
            break;
    }

    return (
        <>
            <span className={styles.task_temp}>Срок: &nbsp;</span>
            <span className={styles.task_temp}>{taskTemp}</span>
        </>
    );
}
