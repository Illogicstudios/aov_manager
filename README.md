# AOV Manager

AOV Manager is a Maya tool to create light groups and AOVs easily

## How to install

You must specify the correct path of the installation folder in the template_main.py file :
```python
if __name__ == '__main__':
    # TODO specify the right directory
    install_dir = 'PATH/TO/aov_manager'
    # [...]
```

---

## Features
<div align="center">
  <span>
    <img src="https://user-images.githubusercontent.com/94440879/215740855-986244f0-ecc9-4713-a091-17a1c85e4ca2.png" width=41%>
  </span>
  
  <span>
    <img src="https://user-images.githubusercontent.com/94440879/215742613-aced2dd1-7d28-41f1-ad3b-c2e72e4e1e63.png" width=55%>
  </span>
  <p>Scene with a sphere and 3 lights (one red, one green and one blue)</p>
  <br/>
</div>

### Light Group Part

<div align="center">
  <span>
    <img src="https://user-images.githubusercontent.com/94440879/215744863-0b25ab6a-0fc9-4142-8bb8-201b7592cd0f.png" width=50%>
  </span>
  <p weight="bold">Light Group part with a light group with the red light and another light group will be created with the green and blue light</p>
  <br/>
</div>

In this part light groups can be created. Lights on the left have to be selected to create a new light group.

The button "Create a light group by light" place each light alone in a light group

To add a light selected on the left in a light group selected on the right there is the button "Add to light group selected"

Light can be removed from a light group and light group can be also removed

### AOVs Part

<div align="center">
  <span>
    <img src="https://user-images.githubusercontent.com/94440879/215746625-37be77f6-734d-4937-8d12-5dc5f3bbac12.png" width=50%>
  </span>
  <p weight="bold">AOV part with all the aov availables on the leftt</p>
  <br/>
</div>


<div align="center">
  <span>
    <img src="https://user-images.githubusercontent.com/94440879/215746878-08dbfb80-4526-46fd-aed0-f44e131ecc9b.png" width=39%>
  </span>
  <span>
    <img src="https://user-images.githubusercontent.com/94440879/215746997-9bc0fb18-a6c2-467f-bc90-c8c1428614df.png" width=59%>
  </span>
  <p weight="bold">Light group AOVs and N AOV have been activated and the green and blue lights light group AOV is selected</p>
  <br/>
</div>


In this part available AOVs are on the left and activated ones are on the right. The 2 buttons with arrows can be clicked to toggle the activation of selected AOVs. When AOVs are activated, they can be selected in the Arnold RenderView.









