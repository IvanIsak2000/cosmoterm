# cosmoterm

Terminal messenger using p2p technologies
(project is currently *in development*)

![logo](https://github.com/IvanIsak2000/cosmoterm/assets/79650307/44c94073-9c72-4edc-93a1-9e6308b72da0)





## Usage HOWTO

### Read messages
```bash
python3 cosmoterm.py --r
.....

```
Tell a friend your IP and port number

### Send messages
```bash
python3 cosmoterm.py --s
.....

```

<hr>

## Example

### 1. Await
To receive a message, you need to enable the server part of the program:

```bath
Your IP:  <your IP>
Enter a your server port (default 5000 [press enter]): <enter port / press enter (default 5000)>
To receive a message, your friend must enter your IP into the program
We are waiting for messages...
<connection waiting>
```


### 2. Send

Let's say we want to send a message to a friend, for this open the terminal and write:
```bash 

python3 cosmoterm.py --s



       :BG:
      ?@@@&7                                                                                                               :Y
     J@@@@@@?                                                                                                              !&
    :@@&GG&@&.           .!JJJJJ7:         .7JJJJJ7:         :?JJJJJ7.      ?^ !?JJYJ^  .!?JJYJ~          ^?JJJJJ~       7?G&J?J~       ^?JJJJJ!.       ~7 ^?JY~   ~? ^?JJYY!   ~?JJYY7.
    J@@^  ~@@!         .PP~.   .^5B:     .GP^.   .^5G.      GP:    .!B7     ##J^    :GG75^    :P#.      !B?:    .7BJ       7&.        ^BY:    .!G5      5&57.      Y&Y~.   .J#!5~.   .?&^
    ?@@BJY#@@~        .&7         ?P    :&7         !&:    ~@        .:     #B        &#        #5     Y#.         GG      !&        7&.         YB     Y&.        Y&.       5@.       J&
    !@@@@@@@@:        GP                B5           Y#     GG~.            #Y        B5        PB    :@:           &!     !&       .&!          .&?    YB         Y#        ?&        !&
    :@@@@@@@&         &7                &~           ~&.     :7JYYYJ7.      #Y        BP        PG    7&            B5     !&       ^@Y?JJJJJJJJJ?5~    YB         Y#        ?&        !&
  .?.&@@@@@@G:5.      BP                #Y           J#            .~B5     #Y        BP        PG    ^@.           &7     !&       .&^                 YB         Y#        ?&        !&
  &@^G@@@@@@J7@B      :&!         !P    ^&~         ^&^    ^.        .@:    #Y        BP        PG     PB          PB      !&        ?#.          .     YB         Y#        ?&        !&
  #&^!#&&&#B:!&Y       :B5^     :Y#^     :BY:     :YB^     7#!.     ^GP     #Y        BP        GB      ?B7.    .~G5       .&?        !B?.     .?B!     5#         Y#        ?&        !&
  .   ^JJJ?.             :?YJJJYJ^         ^?YJJJY?^        .7JJJJJJ?:      J~        ?!        7?        !JYJJYJ7.         .?YYY.      ~JYJJJYJ~       !J         ~J        ^Y        :5
      .Y .5
      ~P .B.
       ~YY.



Enter  a friend IP: <write friend IP> 
Your friend with IP <friend IP> online!
Enter your message: HELLO!
Message sent successfully!
```

### 3. Get

```
[<friend IP>] [2023-05-19 09:44:57]: HELLO!
```

       
### 4. Add in history (automatically)
       
```
#history.toml
       
[<friend IP>]
"2023-05-19 09:44:57" = "HELLO!"      
 ```
       


## Found a bug?

It's possible to submit a bug report or a feature request via GitHub [issues](https://github.com/IvanIsak2000/cosmoterm/issues/new)

## Contribution

Checkout [contributing guidelines](docs/CONTRIBUTING.md)





