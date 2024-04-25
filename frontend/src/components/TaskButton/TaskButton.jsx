import styles from './TaskButton.module.scss'

/**
 * Компонент кнопки принимает следующие пропсы:
 * @param {string} taskStatus - Статус задачи. <br/>
 *   Может принимать следующие значения: <br/>
 *   - "active": задача находится в процессе выполнения. В CSS соответствует классу 'active'.<br/>
 *   - "completed": задача выполнена. В CSS соответствует классу 'completed'.<br/>
 *   - "overdue": задача просрочена. В CSS соответствует классу 'overdue'.<br/>
 * @param {string} taskButtonName - имя кнопки. Не обязательный параметр.
 * @param {string} buttonFunctionName - название функции, вызываемой при нажатии кнопки
 */

export function TaskButton({taskStatus, taskButtonName, buttonFunctionName}) {
    const currentTaskStatus = styles[taskStatus];
    const baseBtnClass = styles.task_btn;
    const btnClassName = `${baseBtnClass} ${currentTaskStatus}`
        
    return (
        <>
        <button className={btnClassName} onClick={buttonFunctionName}>{taskButtonName}</button>
        </>
    )
}