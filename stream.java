//How to stream with android studio ---> Link description below

//https://code.tutsplus.com/tutorials/streaming-video-in-android-apps--cms-19888


 android.net.Uri;
import android.widget.MediaController;
import android.widget.VideoView;

<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:paddingBottom="@dimen/activity_vertical_margin"
    android:paddingLeft="@dimen/activity_horizontal_margin"
    android:paddingRight="@dimen/activity_horizontal_margin"
    android:paddingTop="@dimen/activity_vertical_margin"
    android:background="#000000"
    tools:context=".MainActivity" >
 
    <VideoView
        android:id="@+id/myVideo"
        android:layout_width="fill_parent"
        android:layout_height="fill_parent"
        android:layout_centerInParent="true" />
         
</RelativeLayout>
