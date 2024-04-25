import axios from "axios";
import React, { useEffect, useState } from "react";
import { TaskCard } from "../TaskCard/TaskCard";
import styles from "./UserTaskComponent.module.scss";

const API_URL = "http://127.0.0.1:8000/demo/api/tasks/";
const componentClassName = `task_area ${styles.task_area_grid}`;

export function UserTaskComponent() {
    const [tasks, setTasks] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(API_URL, {
                    headers: {
                        Authorization:
                            "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEyNzExMTI1LCJpYXQiOjE3MTI2ODQxMjUsImp0aSI6IjgyNGUxMGJmMGZkZjQ2YzlhOTUxYjJlNjc1OTQwNmYyIiwidXNlcl9pZCI6MX0.iq-lr-SSaT5kN-L49dy221te8jtriepf-i2F8v6ARCY",
                    },
                });
                response.data.map((item) => {
                    if (item.completed) {
                        item.status = "completed";
                    } else {
                        const dateFromServer = new Date(item.date);
                        const currentDate = new Date();
                        if (dateFromServer >= currentDate) {
                            item.status = "active";
                        } else {
                            item.status = "overdue";
                        }
                    }
                });
                setTasks(response.data);
            } catch (error) {
                console.error(error);
            }
        };

        fetchData();
    }, []);

    return (
        <div className={componentClassName}>
            {tasks.map((task) => (
                <TaskCard
                    key={task.id}
                    taskStatus={task.status}
                    taskHeading={task.id}
                    taskContent={task.description}
                    taskDate={task.date}
                />
            ))}
        </div>
    );
}
