import sqlite3

DB_NAME = "health_space.db"


# =========================
# 创建数据库和数据表
# =========================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 用户个人档案表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        name TEXT,
        gender TEXT,
        age INTEGER,
        height REAL,
        weight REAL
    )
    """)

    # BMI / 健康历史记录表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS health_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        record_time TEXT,
        gender TEXT,
        age INTEGER,
        height REAL,
        weight REAL,
        bmi REAL,
        status TEXT,
        score INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_tasks (
        username TEXT,
        task_date TEXT,
        task_name TEXT,
        done INTEGER DEFAULT 0,
        PRIMARY KEY (username, task_date, task_name)
    )
    """)

    conn.commit()
    conn.close()


# =========================
# 保存 / 更新个人档案
# =========================
def save_profile(name, gender, age, height, weight):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 先查这个用户是否已经存在
    cursor.execute("""
    SELECT 1
    FROM profiles
    WHERE name = ?
    """, (name,))

    result = cursor.fetchone()

    if result:
        # 已经存在，就更新
        cursor.execute("""
        UPDATE profiles
        SET gender = ?,
            age = ?,
            height = ?,
            weight = ?
        WHERE name = ?
        """, (
            gender,
            age,
            height,
            weight,
            name
        ))

    else:
        # 不存在，就新增
        cursor.execute("""
        INSERT INTO profiles
        (name, gender, age, height, weight)
        VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            gender,
            age,
            height,
            weight
        ))

    conn.commit()
    conn.close()


# =========================
# 查询个人档案
# =========================
def get_profile(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name, gender, age, height, weight
    FROM profiles
    WHERE name = ?
    """, (name,))

    row = cursor.fetchone()

    conn.close()

    return row


# =========================
# 保存一次健康记录
# =========================
def save_health_record(username, record):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO health_records
    (username, record_time, gender, age, height, weight, bmi, status, score)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        username,
        record["date"],
        record["gender"],
        record["age"],
        record["height"],
        record["weight"],
        record["bmi"],
        record["status"],
        record["score"]
    ))

    conn.commit()
    conn.close()


# =========================
# 查询健康历史
# =========================
def get_health_records(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        record_time,
        gender,
        age,
        height,
        weight,
        bmi,
        status,
        score
    FROM health_records
    WHERE username = ?
    ORDER BY id
    """, (username,))

    rows = cursor.fetchall()

    conn.close()

    return rows

def get_tasks(username, task_date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT task_name, done
    FROM daily_tasks
    WHERE username = ? AND task_date = ?
    """, (username, task_date))

    rows = cursor.fetchall()

    # 第一次使用当天任务时，自动创建
    if not rows:
        tasks = [
            "喝水 至少1500 ml",
            "步行 6000➕ 步",
            "吃够  水果和蔬菜",
            "23:30 前睡觉"
        ]

        for task in tasks:
            cursor.execute("""
            INSERT INTO daily_tasks
            (username, task_date, task_name, done)
            VALUES (?, ?, ?, 0)
            """, (
                username,
                task_date,
                task
            ))

        conn.commit()

        rows = [
            (task, 0)
            for task in tasks
        ]

    conn.close()

    return {
        task_name: bool(done)
        for task_name, done in rows
    }


def save_task(username, task_date, task_name, done):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE daily_tasks
    SET done = ?
    WHERE username = ?
      AND task_date = ?
      AND task_name = ?
    """, (
        int(done),
        username,
        task_date,
        task_name
    ))

    conn.commit()
    conn.close()


# 启动时创建数据库和表
init_db()