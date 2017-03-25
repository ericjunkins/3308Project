package com.example.lerrrrmps.myfirstapp;

import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.PorterDuff;
import android.view.MotionEvent;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.util.AttributeSet;
import android.content.Context;
import android.view.View;

public class ControlStickViewRight extends SurfaceView implements SurfaceHolder.Callback, View.OnTouchListener {

    private float centerX;
    private float centerY;
    private float baseRadius;
    private float hatRadius;
    //public JoystickListener joystickCallback;

    public ControlStickViewRight(Context context){
        super(context);
        getHolder().addCallback(this);
        setOnTouchListener(this);
    }

    public ControlStickViewRight(Context context, AttributeSet attributes, int style){
        super(context,attributes,style);
        getHolder().addCallback(this);
        setOnTouchListener(this);
    }

    public ControlStickViewRight(Context context, AttributeSet attributes){
        super(context, attributes);
        getHolder().addCallback(this);
        setOnTouchListener(this);
    }

    @Override
    public void surfaceCreated(SurfaceHolder holder){
        setupDimensions();
        drawJoystick(centerX,centerY);
    }
    @Override
    public void surfaceChanged(SurfaceHolder holder, int forsat, int width, int height){
    }

    @Override
    public void surfaceDestroyed(SurfaceHolder holder){
    }

    private void setupDimensions(){
        centerX = getWidth() / (float)1.5;
        centerY = getHeight() / 2;
        baseRadius = Math.min(getWidth(), getHeight()) / 3;
        hatRadius = Math.min(getWidth(), getHeight()) / 5;
    }

    private void drawJoystick(float newX, float newY){
        int alpha = 255;
        int red = 100;
        int blue = 100;
        int green = 100;
        int ratio = 5;
        if(getHolder().getSurface().isValid()) {
            Canvas myCanvas = this.getHolder().lockCanvas();
            Paint colors = new Paint();
            myCanvas.drawColor(Color.TRANSPARENT, PorterDuff.Mode.CLEAR);

            float hypotenuse = (float) Math.sqrt(Math.pow(newX-centerX,2) + Math.pow(newY - centerY,2));
            float sin = (newY - centerY)/hypotenuse;
            float cos = (newX - centerX)/hypotenuse;

            for (int i = 1; i <= 100; i++) {
                colors.setARGB(100 , i*(255/100) , i* (255/100) , i* (255/100));
                myCanvas.drawCircle(centerX, centerY, i*baseRadius/100, colors);
            }
            for (int i =1; i <= (int) (baseRadius/ratio); i++){
                colors.setARGB(255/i,20,20,20);
                myCanvas.drawCircle(newX-cos*hypotenuse* (ratio/baseRadius)*i,
                        newY - sin *hypotenuse * (ratio/baseRadius)* i, i*(hatRadius * ratio/baseRadius),colors);
            }
            colors.setARGB(255,0,0,0);
            myCanvas.drawCircle(newX,newY,hatRadius+ (int) 0.2* hatRadius,colors );
            for(int i =0; i<= (int)( hatRadius/ratio);i++) {
                colors.setARGB(255, (int) (i* (255*(ratio/hatRadius))), (int) (i* (100 *ratio/baseRadius)),
                        (int) (i* (100 *ratio/baseRadius)));
                myCanvas.drawCircle(newX, newY, hatRadius - (float) i * ratio/2, colors);
            }
            getHolder().unlockCanvasAndPost(myCanvas);
        }
    }

    @Override
    public boolean onTouch(View view, MotionEvent myEvent){
        if (view.equals(this)) {
            if (myEvent.getAction() != myEvent.ACTION_UP) {
                float displacement = (float) Math.sqrt(Math.pow(myEvent.getX() - centerX, 2)+ Math.pow(myEvent.getY() - centerY,2));
                if (displacement < baseRadius) {
                    drawJoystick(centerX, myEvent.getY());
                    ///joystickCallback.onJoystickMoved((myEvent.getX() - centerX) / baseRadius, (myEvent.getY() - centerY) / baseRadius, getId());
                }
                else{
                    float ratio = baseRadius/displacement;
                    float constrainedX = centerX + (myEvent.getX()-centerX)*ratio;
                    float constrainedY = centerY + (myEvent.getY()-centerY)*ratio;
                    drawJoystick(centerX,constrainedY);
                }
            } else {
                drawJoystick(centerX, centerY);
            }
        }
        return true;
    }

    public interface JoystickListener {
        void onJoystickMoved(float xPercent, float yPercent, int source);
    }
}
