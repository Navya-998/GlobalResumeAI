async function generateSummary() {

    const name = document.querySelector('[name="full_name"]').value;

    const companies = document.querySelectorAll('[name="company[]"]');
    const titles = document.querySelectorAll('[name="job_title[]"]');
    const durations = document.querySelectorAll('[name="duration[]"]');
    const descriptions = document.querySelectorAll('[name="job_description[]"]');

    let experience = "";

    for (let i = 0; i < companies.length; i++) {

        experience +=
            "Company: " + companies[i].value + "\n" +
            "Job Title: " + titles[i].value + "\n" +
            "Duration: " + durations[i].value + "\n" +
            "Description: " + descriptions[i].value + "\n\n";

    }

    try {

        const response = await fetch("/generate-summary", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                name: name,
                role: "",
                experience: experience

            })

        });

        const data = await response.json();

        document.getElementById("summary").value = data.summary;

    } catch (error) {

        console.error(error);
        alert("Unable to generate AI summary.");

    }

}

function addExperience() {

    const container = document.getElementById("experience-container");

    const item = container.firstElementChild.cloneNode(true);

    item.querySelectorAll("input").forEach(input => input.value = "");
    item.querySelectorAll("textarea").forEach(textarea => textarea.value = "");

    container.appendChild(item);

}