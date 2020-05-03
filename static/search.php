<?php
    $key=$_GET['key'];
    $array = array();
    $con=mysqli_connect("35.245.115.59","root","dwdstudent2015","streamline");
    $query=mysqli_query($con, "SELECT * FROM IMDb_Catalog WHERE title LIKE '%{$key}%'");
    while($row=mysqli_fetch_assoc($query))
    {
      $array[] = $row['title'];
    }
    echo json_encode($array);
    mysqli_close($con);
?>
