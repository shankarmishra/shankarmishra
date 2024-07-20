const express = require('express');
const app = express();
const path = require('path');
const usermodel = require('./model/user');


const mongoose = require('mongoose');
let url = "mongodb://localhost:27017/userdetails";
mongoose.connect(url);
const db = mongoose.connection

db.on("connected", () => {
     console.log("connected successfuly");
})
db.on("error", () => {
     console.log("some error");
})
db.on("disconnected", () => {
     console.log("disconnected");
})

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));
app.set('view engine', 'ejs');

app.get('/', (req, res) => {
     res.render('../view/login');

})
app.get('/createaccount', async(req, res) =>{
     res.render('../view/createaccount');
})



app.get('/read', async (req, res) => {
     let user = await usermodel.find();
     res.render('../view/read', { user });


})
app.post('/create', async (req, res) => {
     const { username, password } = req.body;

     const createduser = await usermodel.create({
          username,
          password,
     })
     res.redirect('/read');
})

const PORT = process.env.PORT || 4000;
const server = app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});