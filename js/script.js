/* =========================
   SMART TIMETABLE
========================= */

function addTask(){

let input = document.getElementById("taskInput");

if(!input) return;

let task = input.value;

if(task === "") return;

let li = document.createElement("li");

li.className = "list-group-item";

li.innerHTML = task + 
" <button onclick='removeItem(this)' style='float:right' class='btn btn-sm btn-danger'>Delete</button>";

document.getElementById("taskList").appendChild(li);

input.value="";

}

/* =========================
   HABIT TRACKER
========================= */

function addHabit(){

let input = document.getElementById("habitInput");

if(!input) return;

let habit = input.value;

if(habit === "") return;

let li = document.createElement("li");

li.className = "list-group-item";

li.innerHTML = habit + 
" <button onclick='removeItem(this)' style='float:right' class='btn btn-sm btn-danger'>Done</button>";

document.getElementById("habitList").appendChild(li);

input.value="";

}

/* =========================
   GOAL PLANNER
========================= */

function addGoal(){

let input = document.getElementById("goalInput");

if(!input) return;

let goal = input.value;

if(goal === "") return;

let li = document.createElement("li");

li.className = "list-group-item";

li.innerHTML = goal + 
" <button onclick='removeItem(this)' style='float:right' class='btn btn-sm btn-success'>Complete</button>";

document.getElementById("goalList").appendChild(li);

input.value="";

}

/* =========================
   IDEA VAULT
========================= */

function addIdea(){

let input = document.getElementById("ideaInput");

if(!input) return;

let idea = input.value;

if(idea === "") return;

let li = document.createElement("li");

li.className = "list-group-item";

li.innerHTML = idea + 
" <button onclick='removeItem(this)' style='float:right' class='btn btn-sm btn-warning'>Saved</button>";

document.getElementById("ideaList").appendChild(li);

input.value="";

}

/* =========================
   REMOVE ITEM
========================= */

function removeItem(button){

button.parentElement.remove();

}