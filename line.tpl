% from datetime import datetime as dt
% import time

   <table border=0>
   % for ch, line_dct in rows.items():
       <tr bgcolor="#ddd"><th>{{ch}}</th>
       % for prog_id, times in line_dct.items():
           % title, start, end = times
           % start = str(dt.strptime(time.ctime(int(start) / 1000), '%a %b %d %H:%M:%S %Y'))
           % end = str(dt.strptime(time.ctime(int(end) / 1000), '%a %b %d %H:%M:%S %Y'))
               <td>{{title}}<br>{{start}}<br>{{end}}</td>
       % end
     </tr>
   % end
   </table>
