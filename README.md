RES = (360, 640) => 720, 1280  

monkey: r = 40px  
monkey sprite: anchor x: 2/3 (tail: 40px, head: 80px)  

pipe head: x = 120px, y = 90px  
pipe gap: 160-200px  

sand floor: y = 100px  

### flappy-seamonkai

The boosted seamonkai flappying around.  

### Software Requirements

- Python 3.7  
> sudo apt-get update && sudo apt-get install build-essential libpq-dev libssl-dev openssl libffi-dev sqlite3 libsqlite3-dev libbz2-dev zlib1g-dev cmake python3.7 python3-pip python3.7-dev python3.7-venv  

- venv  
> mkdir venv && python3.7 -m venv venv/  
> source venv/bin/activate  
> deactivate  

- pyglet, gym, torch, tensorboard, msgpack, wheel  
> (venv) pip3 install 'pyglet==1.5.0' gym torch tensorboard 'msgpack==1.0.2' wheel --no-cache-dir  
