css = """
<style>
section[data-testid="stSidebar"] {
    display: none;
}

/* Center container */
.center-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-top: 100px;
}

.center-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 85vh;
}

.form-card {
    width: 420px;
    padding: 30px;
    border-radius: 16px;
    background: rgba(17, 24, 39, 0.85);
    border: 1px solid rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
}

.signup-link {
    text-align: center;
    margin-top: 15px;
    font-size: 14px;
}


/* Title styling */
.title {
    font-size: 48px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 10px;
}

/* Subtitle styling */
.subtitle {
    font-size: 20px;
    color: #9ca3af;
    text-align: center;
}

section[data-testid="stSidebar"] {
    display: none;
}


/* Center whole block vertically */
.block-container {
    padding-top: 5vh;
}

/* Card */
.form-card {
    padding: 35px;
    border-radius: 18px;
    background: rgba(17, 24, 39, 0.9);
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}

/* Title */
.title {
    text-align: center;
    font-size: 34px;
    font-weight: 600;
    margin-bottom: 6px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    font-size: 15px;
    color: #9ca3af;
    margin-bottom: 25px;
}

/* Signup link */
.signup-text {
    text-align: center;
    font-size: 14px;
    margin-top: 18px;
    color: #9ca3af;
}

/* Make button look like link */
.link-button > button {
    background: none;
    border: none;
    color: #3b82f6;
    text-decoration: underline;
    cursor: pointer;
    padding: 0;
    font-size: 14px;
}
.link-button > button:hover {
    color: #60a5fa;
}

</style>
"""
