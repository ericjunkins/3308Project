package com.example.lerrrrmps.myfirstapp;

import android.annotation.SuppressLint;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.LinearGradient;
import android.graphics.Paint;
import android.graphics.PorterDuff;
import android.graphics.RectF;
import android.graphics.Shader;
import android.util.Log;
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
    public JoystickListener joystickCallback;

    public ControlStickViewRight(Context context){
        super(context);
        getHolder().addCallback(this);
        setOnTouchListener(this);
        if(context instanceof JoystickListener)
            joystickCallback = (JoystickListener) context;
    }

    public ControlStickViewRight(Context context, AttributeSet attributes, int style){
        super(context,attributes,style);
        getHolder().addCallback(this);
        setOnTouchListener(this);
        if(context instanceof JoystickListener)
            joystickCallback = (JoystickListener) context;
    }

    public ControlStickViewRight(Context context, AttributeSet attributes){
        super(context, attributes);
        getHolder().addCallback(this);
        setOnTouchListener(this);
        if(context instanceof JoystickListener)
            joystickCallback = (JoystickListener) context;
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
        centerX = getWidth() / 2;
        centerY = getHeight() / 2;
        baseRadius = Math.min(getWidth(), getHeight()) / 3;
        hatRadius = Math.min(getWidth(), getHeight()) / 4;
    }

    @SuppressLint("NewApi")
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

            Shader shader = new LinearGradient(centerX,centerY ,centerX,centerY+ getHeight()/2, Color.BLUE, Color.BLACK, Shader.TileMode.CLAMP);
            Paint paint = new Paint();
            paint.setShader(shader);
            myCanvas.drawRect(new RectF(0, centerY + getHeight()/2, centerX + getWidth()/2 , centerY), paint);

            Shader shader2 = new LinearGradient(centerX,centerY,centerX,centerY - getHeight()/2, Color.BLUE, Color.BLACK, Shader.TileMode.CLAMP);
            paint.setShader(shader2);
            myCanvas.drawRect(new RectF(centerX - getWidth()/2, centerY, centerX + getWidth()/2 , centerY - getHeight()/2), paint);


            colors.setARGB(255,255,255,255);
            myCanvas.drawOval(centerX-getWidth()/4, centerY + getHeight()/3, centerX + getWidth()/4, centerY - getHeight()/3, colors);

            for (int i = 1; i <= 100; i++) {
                colors.setARGB(100 , i*(255/100) , i* (255/100) , i* (255/100));
                myCanvas.drawOval(centerX - getWidth()/5, centerY + getHeight()/4, centerX + getWidth()/5, centerY - getHeight()/4, colors);
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
                int height = getHeight()/3;
                float displacement = (float) Math.sqrt(Math.pow(myEvent.getY() - centerY, 2));
                //Log.d("maths","CX: " + centerX + " CY: " + centerY + "base radius" + baseRadius);
                if (displacement < height) {
                    drawJoystick(centerX, myEvent.getY());
                    joystickCallback.onJoystickMoved((myEvent.getX() - centerX)/height, (myEvent.getY() - centerY)/height, getId());
                }
                else{
                    float ratio = height/displacement;
                    float constrainedX = centerX + (myEvent.getX()-centerX)*ratio;
                    float constrainedY = centerY + (myEvent.getY()-centerY)*ratio;
                    drawJoystick(centerX,constrainedY);
                    joystickCallback.onJoystickMoved((constrainedX-centerX)/height, (constrainedY-centerY)/height, getId());
                }
            } else {
                drawJoystick(centerX, centerY);
                joystickCallback.onJoystickMoved(0,0,getId());
            }
        }
        return true;
    }

    public interface JoystickListener {
        void onJoystickMoved(float xPercent, float yPercent, int id);
    }
}
