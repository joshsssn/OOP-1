get_name() {
  echo $USER
}

if [[ $OSTYPE == "linux-gnu" ]]; then
    echo "Linux detected" 
    echo "Hello, $(get_name)"
fi 

if [[ $(get_name) == "kali" ]]; then
    echo "Btw you are using Kali Linux..."
    echo -e "you f**king \e[1m\e[31mscript kiddie\e[0m\e[0m"
fi
