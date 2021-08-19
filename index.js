const express = require('express')
const app = express()

const MongoClient = require('mongodb').MongoClient;
const uri = process.env.MONGODB_URI;
const dbName = 'data_sorare';
const {spawn} = require('child_process');
const port = process.env.PORT || 3000;

let db

MongoClient.connect(uri, function(err, client) {
  console.log("Connected successfully to server");
  db = client.db("data_sorare");
});

app.get('/players/:player', async (req,res) => {
    try {
		const id = req.params.player
        const docs = await db.collection('players').find({"player_name":id}).toArray()
        res.status(200).json(docs)
    } catch (err) {
        console.log(err)
        throw err
    }
})

app.get('/update', (req, res) => {

	var dataToSend;
	const python = spawn('python', ['./script/crawl_understats_players.py']);
	python.stdout.on('data', function (data) {
	console.log('python script');
	dataToSend = data.toString();
	});
	python.on("close", (code) => { console.log ('process close &{code}');
	res.send(dataToSend)
	});
	})

app.listen(port,'0.0.0.0',  () => {
    console.log("Serveur à l'écoute")
})