function toggleHide(targetId){
  let target = document.getElementById(targetId);

  if(target.classList.contains("hide")) {
    target.classList.remove("hide");
  } else {
    target.classList.add("hide");
  }
}

function toggleNewTask(){
  toggleHide("new-button");
  toggleHide("new-card");
};

function toggleUpdateTask(id){
  toggleHide(`task-${id}-content`);
  toggleHide(`task-${id}-update`);
};

function cancelNewTask(){
  let input = document.getElementById("content");
  input.value = "";
  toggleNewTask();
}

function updateCompleted(id) {
  // Get the checkbox
  let checkBox = document.getElementById(`task-${id}-completed`);

  fetch(`http://127.0.0.1:5000/task/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ completed: checkBox.checked })
  })
    .then(response => response.json())
    .then(data => {
      console.log(data);
    })
    .catch(error => {
      let target = document.getElementById("error-box");
      target.innerHTML = "An error occured, unable to update status!";
      setTimeout(()=>{ target.innerHTML = ""}, 2000)
      console.error('通信に失敗しました', error);
    });
}

function updateTask(id) {
  let input = document.getElementById(`task-${id}-update-input`);

  fetch(`http://127.0.0.1:5000/task/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content: input.value })
  })
    .then(response => response.json())
    .then(data => {
      console.log(data)
      let target = document.getElementById(`task-${id}-content`);
      target.innerHTML = data["content"];
  });

  toggleUpdateTask(id);
}
