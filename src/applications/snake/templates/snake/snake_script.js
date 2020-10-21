{% load static %}


const canvas = document.getElementById('snake');
const ctx  = canvas.getContext('2d');

const ground = new Image();
ground.src = "{% static 'snake/Snake_background.png' %}";

const foodIMG = new Image();
foodIMG.src= "{% static 'snake/snake_food.png' %}";


const snakeHead = new Image();
snakeHead.src ="{% static 'snake/head.png' %}";

const snakeTail = new Image();
snakeTail.src ="{% static 'snake/Tail.png' %}";


let box = 32;

let score = 0;

let food = {
    x: Math.floor(Math.random() * 17 + 1 ) * box,
    y: Math.floor(Math.random() * 15 + 3 ) * box,
};

let snake =[];
snake[0] = {
    x: 9* box,
    y: 10* box,
};

document.addEventListener("keydown", direction);

let dir;

function direction(event){
    if(event.keyCode == 37 && dir != "right")
        dir = "left";
    else if(event.keyCode == 38 && dir != "down")
        dir = "up";
    else if(event.keyCode == 39 && dir != "left")
        dir = "right";
    else if(event.keyCode == 40 && dir != "up")
        dir = "down";
    else if(event.keyCode == 13){
        clearInterval(game);
        snake=[];
        snake[0] = {
        x: 9* box,
        y: 10* box,
    };
        dir = null;
        score = 0;
        game = setInterval(drawGame, 90)
    }

}

function eatTail(head, arr){
    for(let i = 0; i < arr.length; i++){
        if(head.x == arr[i].x && head.y ==arr[i].y)
            clearInterval(game);
    }
}
function drawGame(){
    ctx.drawImage(ground, 0,0);

    ctx.drawImage(foodIMG, food.x, food.y);

    for(let i = 0; i< snake.length;i++){
        if(i == 0){
            ctx.drawImage(snakeHead, snake[i].x, snake[i].y);
        }
        else{
            ctx.drawImage(snakeTail,snake[i].x, snake[i].y);
        }
    }

    ctx.fillStyle = "white";
    ctx.font = "50px Arial";
    ctx.fillText("Score: " + score, box, box * 1.7);

    let snakeX = snake[0].x;
    let snakeY = snake[0].y;

    if(snakeX == food.x && snakeY== food.y){
        score++;
        food = {
    x: Math.floor(Math.random() * 17 + 1 ) * box,
    y: Math.floor(Math.random() * 15 + 3 ) * box,
    };
    } else {
        snake.pop();
    }

    if(snakeX < 0 - box || snakeX>box*19 || snakeY< box*3 || snakeY > box * 19)
        clearInterval(game);


    if(dir == "left") snakeX -= box;
    if(dir == "right") snakeX += box;
    if(dir == "up") snakeY -= box;
    if(dir == "down") snakeY += box;

    let newHead = {
        x: snakeX,
        y: snakeY,
    };

    eatTail(newHead, snake);

    snake.unshift(newHead);
}

let game = setInterval(drawGame, 90);