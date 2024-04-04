/**
 * Компонент карточки задачи.
 * Принимаемые пропсы:
 * @param {string} taskStatus - Статус задачи. <br/>
 *   Может принимать следующие значения: <br/>
 *   - "active": задача находится в процессе выполнения. В CSS соответствует классу 'active'.<br/>
 *   - "completed": задача выполнена. В CSS соответствует классу 'completed'.<br/>
 *   - "overdue": задача просрочена. В CSS соответствует классу 'overdue'.<br/>
 * @param {string} taskHeading - заголовок задачи.
 * @param {string} taskContent - текст задачи.
 */

import styles from "./TaskCard.module.scss";

import { TaskButton } from "../TaskButton/TaskButton";
import { TaskTemp } from "../TaskTemp/TaskTemp";

export function TaskCard({ taskHeading, taskContent, taskStatus }) {

    let containerClassName = `${styles.task_container} ${styles[taskStatus]}`

    let taskButtonName = "";

    switch (taskStatus) {
        case "active":
            taskButtonName = "Выполнить задание";
            break;
        case "overdue":
            taskButtonName = "Выполнить задание";
            break;
        case "completed":
            taskButtonName = "Посмотреть задание";
            break;
        default:
            taskButtonName = "";
            break;
    }

    return (
        <div className={styles.task_item}>
            <div className={containerClassName}>
                <h3 className={styles.task_heading}>{taskHeading}</h3>
                <p className={styles.task_content}>{taskContent}</p>
                <div className={styles.task_management}>
                   <div> <TaskTemp /></div>
                    <div><TaskButton
                        taskStatus={taskStatus}
                        taskButtonName={taskButtonName}
                    /></div>
                </div>
            </div>
        </div>
    );
}
