def diagram_to_steps(text):
    lines = text.split("\n")
    steps = []

    for i, line in enumerate(lines):
        if line.strip():
            steps.append(f"Step {i+1}: {line}")

    return steps