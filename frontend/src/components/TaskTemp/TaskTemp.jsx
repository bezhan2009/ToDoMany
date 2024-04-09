import styles from "./TaskTemp.module.scss";

const taskTempClassName = `${styles.task_temp} ${styles.task_temp_value}`;

export function TaskTemp({ taskStatus, taskDate }) {
    let taskTemp = "";

    if (taskStatus === "overdue") {
        taskTemp = "исчерпан";
    } else if (taskStatus === "completed") {
        taskTemp = "выполнено";
    } else {
        const dateFromServer = new Date(taskDate);
        const currentDate = new Date();
        if (
            dateFromServer.getDate() === currentDate.getDate() &&
            dateFromServer.getMonth() === currentDate.getMonth() &&
            dateFromServer.getFullYear() === currentDate.getFullYear()
        ) {
            taskTemp = "сегодня";
        } else if (dateFromServer.getDate() - currentDate.getDate() === 1) {
            taskTemp = "завтра";
        } else {
            taskTemp = `${dateFromServer.getDate()}.${dateFromServer.getMonth()}.${dateFromServer.getFullYear()}`;
        }
    }

    return (
        <>
            <span className={styles.task_temp}>Срок:</span>
            <span className={taskTempClassName}>{taskTemp}</span>
        </>
    );
}
