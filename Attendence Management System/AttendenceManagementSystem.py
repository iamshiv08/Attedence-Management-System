import streamlit as st

overall = 0.75  # 75% overall attendance
indivisual = 0.70  # 70% individual subject attendance

# Subjects total lectures
subjects = {
    "Python": 70,
    "FSD-2": 70,
    "COA": 66,
    "TOC": 50,
    "DM": 60
}

# calculate attendance percentage
def calculate_attendance(attended, total):
    return attended / total

# calculate bunkable lectures
def calculate_bunk_lectures(attended, total, threshold):
    required_attended = threshold * total
    bunk_lectures = attended - required_attended
    return max(0, int(round(bunk_lectures)))

def main():
    st.set_page_config(page_title="Attendance Manager", page_icon="📊")
    st.title("📊 Attendance Management System")
    st.write("Manage your attendance effectively and plan your bunked lectures wisely!")

    # Sidebar for inputs
    with st.sidebar:
        st.header("Input Parameters")
        st.write("### Enter Lectures Attended for Each Subject:")
        attendance = {}
        for subject, total in subjects.items():
            attendance[subject] = st.number_input(f"{subject} (0-{total})", min_value=0, max_value=total, value=0)

    # Calculate total attended lectures
    total_attended = sum(attendance.values())
    overall_attendance_percentage = calculate_attendance(total_attended, sum(subjects.values()))
    overall_bunk_lectures = calculate_bunk_lectures(total_attended, sum(subjects.values()), overall)

    # Calculate individual attendance
    results = {}
    for subject, total in subjects.items():
        attended = attendance[subject]
        individual_attendance_percentage = calculate_attendance(attended, total)
        bunk_lectures_remaining = calculate_bunk_lectures(attended, total, indivisual)
        results[subject] = {
            "attendance_percentage": individual_attendance_percentage,
            "bunk_lectures_remaining": bunk_lectures_remaining,
            "total_lectures": total,
            "total_attended": attended,
            "total_bunked": total - attended
        }

    # Display overall attendance
    st.header("📅 Overall Attendance")
    st.write(f"**Total Lectures:** {sum(subjects.values())}")
    st.write(f"**Total Lectures Attended:** {total_attended}")
    st.write(f"**Total Lectures Bunked:** {sum(subjects.values()) - total_attended}")
    st.write(f"**Overall Attendance Percentage:** {overall_attendance_percentage * 100:.2f}%")
    st.progress(overall_attendance_percentage)
    if overall_attendance_percentage >= overall:
        st.success(f"✅ You can bunk up to **{overall_bunk_lectures}** lectures overall and still maintain 75% attendance.")
    else:
        st.error(f"❌ You need to attend **{int(round(sum(subjects.values()) * overall - total_attended))}** more lectures to reach 75% overall attendance.")

    st.write("---")
    st.subheader("📚 Individual Subject Attendance")
    for subject, total in subjects.items():
        with st.expander(f"**{subject}**"):
            st.write(f"- **Total Lectures:** {results[subject]['total_lectures']}")
            st.write(f"- **Total Lectures Attended:** {results[subject]['total_attended']}")
            st.write(f"- **Total Lectures Bunked:** {results[subject]['total_bunked']}")
            st.write(f"- **Attendance Percentage:** {results[subject]['attendance_percentage'] * 100:.2f}%")
            st.progress(results[subject]['attendance_percentage'])
            if results[subject]['attendance_percentage'] >= indivisual:
                st.success(f"✅ You can bunk up to **{results[subject]['bunk_lectures_remaining']}** lectures and still maintain 70% attendance.")
            else:
                st.error(f"❌ You need to attend **{int(round(total * indivisual - attendance[subject]))}** more lectures to reach 70% attendance.")

if __name__ == "__main__":
    main()