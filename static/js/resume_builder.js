let expCount = 0;

function addExperience(){

expCount++;

document.getElementById("experience-container").innerHTML += `

<div class="card p-3 mt-3">

<input class="form-control mb-2"
name="company${expCount}"
placeholder="Company">

<input class="form-control mb-2"
name="designation${expCount}"
placeholder="Designation">

<input class="form-control mb-2"
name="duration${expCount}"
placeholder="Duration">

<textarea
class="form-control"
name="description${expCount}"
placeholder="Description"></textarea>

</div>

`;

}


let eduCount = 0;

function addEducation(){

eduCount++;

document.getElementById("education-container").innerHTML += `

<div class="card p-3 mt-3">

<input class="form-control mb-2"
name="college${eduCount}"
placeholder="College">

<input class="form-control mb-2"
name="degree${eduCount}"
placeholder="Degree">

<input class="form-control mb-2"
name="year${eduCount}"
placeholder="Year">

</div>

`;

}