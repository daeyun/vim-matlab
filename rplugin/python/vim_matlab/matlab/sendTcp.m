function sendTcp(port, msg)
t = tcpip('localhost'); 
set(t, 'RemotePort', port);

try
    fopen(t);
    fwrite(t, msg,'uchar');
catch
end

fclose(t);