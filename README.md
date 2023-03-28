# Project Weekly MOP

**Author:** Harry Gibbins [fucking legend]

**Runtime:** Python 3.8

**S3 Bucket:** atom-reporting

This repo holds the code for the automation of Powerpoint making for a projects's Weekly MOP deck. Docker image is deployed to ECR via Actions. Updating the code here will cause changes for ALL projects that use this function.

NB: The logic stored here is for a campaign-based MOP report. (For country based, see Hazel Weekly MOP.)

***

## PWPT Text Replacement

The script queries the database and replaces given text in the template with the queried values.

The template is currently held in S3 under `OAK/WEEKLY_MOP/OAKMEG_Pacing_Template.pptx`. This can be altered in future versions via env variables. Text replacement is based on `key:value` pairs. The script loops through the text in each of objects for a given slide and replaces if matched. Text must match in *entirely*; words within a sentence will not be substituted.

***

## PWPT Figures

The `daily_fig_performance` gets passed to the figure function as a dictionary. This builds out a Plotly figure and inserts into a predefined place on the slide (aligns with the borders etc) in the order of `left`, `top`, `width`, `height`. Other figures will be built out in future releases to cover all reporting situations.

For future figures, the easiest way is to find the dimensions outside of the repo. There is the potential to convert from Powerpoint centimeters to the appropriate unit.

***

## AWS Lambda Set-Up

The event from EventsBridge (EVB) is overwritten at runtime. The service passes the `CMP_PROJECT` variable and `S3_OUTPUT_PREFIX` as a Constant. For now, the target is `oakmeg-weekly-mop` Lambda function. See template below for example set-up in EVB.

```json
{
  "CMP_PROJECT": "Nutmeg - PRO-12767",
  "S3_OUTPUT_PREFIX": "NUTMEG/WEEKLY_MOP"
}
```

***

##  TO DO

### **Reporting**

- [ ] Use environment variables to alter:
  - [ ] Between DISPLAY and VIDEO reporting.
  - [ ] Templates for different projects (S3 key)

### **Asset Replacement**

- [ ] Find way to ascertain unique assets from all assets in a campaign
- [x] Find way for insert / deletion of asset templates with actual assets
  - Loop through to get each asset dimensions. Then insert `add_picture()` with them.
  - See logic in Figure insertion

### **Creating and Inserting Figures**

- [x] Build logic for figure building
- [ ] Map building / insertion
  - Build out maps for AOI / country (Plotly or Kepler via png files?)
- [ ] Use `pptx.utils` to convert between Powerpoint centimeters and the corresponding units in Python.
  - Will lead to an easier / less 'hacky' way of inserting figures

### **Misc / If capacity allows**

- [ ] Add tests (and CI GH Action)
- [ ] Look into IaC / CloudFormation for deployment for other projects (Mike / MADS?).
  - On hold until I.T. review AWS CDK
