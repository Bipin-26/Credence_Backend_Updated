const express = require("express");
const mongoose = require("mongoose");
const winston = require("winston")
const bodyParser = require("body-parser")
const router = express.Router()
const app = express()

const movielist= require('./data_modules/data.json')
const server = require('./data_modules/server.json')
const db = require("./data_modules/db.json")

var logger = winston.createLogger({
    level:'info',
    format:winston.format.json(),
    transports: [
      new (winston.transports.Console)(),
      new (winston.transports.File)({ filename: 'log_file.log' })
    ]
  });

if (process.env.NODE_ENV !== 'production') {
logger.add(new winston.transports.Console({
    format: winston.format.simple(),
}));
}

mongoose.connect(`${db['database']}://${db['hostname']}:${db['port']}/${db['dbname']}`);

var movieSchema = new mongoose.Schema({
    name:String,
    img:String,
    summary:String
});

var Movie = mongoose.model("Movie",movieSchema,"moviestore"); 
 
app.get('/display',(req,res)=>{
    try{
        Movie.find({},(err,docs)=>{
            if(err){
                res.send(err)
            }
            else{
                if(docs.length == 0){
                    res.send("No Movies Found")
                    logger.info("No Movies Found")
                }
                else{
                    console.log(docs)
                    res.send("Value found:\n"+docs)
                }  
                
            }
        })
    } catch(err){
        res.send("Something went wrong")
        logger.error(err)
    }
    
})


app.post('/insert',(req,res)=>{
    try{
        Movie.collection.insertMany(movielist,(err,docs)=>{
            if(err){
                logger.error(err)
                res.send("Something went wrong....!!!")
            }
            else{
                res.send("Values inserted successfully")
                logger.info("Values added")
            }
        })
    }
    catch{
        logger.error(err)
    }
})

app.listen(server['port'],()=>{
    console.log(`Server running at http://${server['hostname']}:${server['port']}`);
});


